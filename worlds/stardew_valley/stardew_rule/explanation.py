from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterable, Protocol, Any

from BaseClasses import CollectionState


class ExplainableRule(Protocol):

    @abstractmethod
    def __call__(self, state: CollectionState, context) -> bool:
        ...

    def explain(self, state: CollectionState, context, expected=True) -> RuleExplanation:
        return RuleExplanation(self, state, context, expected)


@dataclass
class RuleExplanation:
    rule: ExplainableRule
    state: CollectionState
    # FIXME
    context: Any
    expected: bool
    sub_rules: Iterable[ExplainableRule] = field(default_factory=set)

    def summary(self, depth=0):
        return "  " * depth + f"{str(self.rule)} -> {self.result}"

    def __str__(self, depth=0):
        if not self.sub_rules:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(RuleExplanation.__str__(i, depth + 1)
                                                      if i.result is not self.expected else i.summary(depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    def __repr__(self, depth=0):
        if not self.sub_rules:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(RuleExplanation.__repr__(i, depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    @cached_property
    def result(self):
        return self.rule(self.state, self.context)

    @cached_property
    def explained_sub_rules(self):
        return [i.explain(self.state, self.context) for i in self.sub_rules]
