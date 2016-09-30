import abc
from typing import TypeVar, Generic, Callable, Tuple

from amino.tc.base import TypeClass, tc_prop
from amino.tc.monad import Monad
from amino.tc.monoid import Monoid
from amino.tc.foldable import Foldable
from amino.tc.applicative import Applicative

F = TypeVar('F')
A = TypeVar('A')
B = TypeVar('B')


class Zip(Generic[F], TypeClass):

    @abc.abstractmethod
    def zip(self, fa: F, fb: F, *fs) -> F:
        ...

    def __and__(self, fa: F, fb: F):
        return self.zip(fa, fb)

    def apzip(self, fa: F, f: Callable[[A], B]) -> F:
        return self.zip(fa, Monad[type(fa)].map(fa, f))

    @tc_prop
    def unzip(self, fa: F) -> Tuple[F, F]:
        tpe = type(fa)
        f = Foldable[tpe]
        m = Monoid[tpe]
        a = Applicative[tpe]
        def folder(z, b):
            l, r = z
            x, y = b
            return m.combine(l, a.pure(x)), m.combine(r, a.pure(y))
        return f.fold_left(fa, (m.empty, m.empty), folder)

__all__ = ('Zip',)
