from uuid import UUID

from shared.domain.types import AssociationIdVO


class TestAssociationIdVO:
    def test_constructor(self) -> None:
        first = UUID("11111111-1111-1111-1111-111111111111")
        second = UUID("22222222-2222-2222-2222-222222222222")
        vo = AssociationIdVO(first, second)

        assert vo.first_id == first
        assert vo.second_id == second

    def test_iter(self) -> None:
        first = UUID("11111111-1111-1111-1111-111111111111")
        second = UUID("22222222-2222-2222-2222-222222222222")
        vo = AssociationIdVO(first, second)

        ids = list(vo)
        assert ids == [first, second]

    def test_str(self) -> None:
        first = UUID("11111111-1111-1111-1111-111111111111")
        second = UUID("22222222-2222-2222-2222-222222222222")
        vo = AssociationIdVO(first, second)

        assert str(vo) == f"{first}/{second}"

    def test_from_tuple(self) -> None:
        first = UUID("11111111-1111-1111-1111-111111111111")
        second = UUID("22222222-2222-2222-2222-222222222222")
        vo = AssociationIdVO.from_tuple((first, second))

        assert vo.first_id == first
        assert vo.second_id == second

    def test_to_tuple(self) -> None:
        first = UUID("11111111-1111-1111-1111-111111111111")
        second = UUID("22222222-2222-2222-2222-222222222222")
        vo = AssociationIdVO(first, second)

        t = vo.to_tuple()
        assert t == (first, second)
