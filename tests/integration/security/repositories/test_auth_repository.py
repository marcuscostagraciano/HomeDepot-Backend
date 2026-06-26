# async def test_authenticate_returns_user_when_credentials_are_valid(
#     auth_repository,
#     persisted_user,
# ):
#     user = await auth_repository.authenticate(
#         persisted_user.email,
#         "123456",
#     )

#     assert user is not None
#     assert user.email == persisted_user.email


# async def test_authenticate_returns_none_when_password_is_invalid(
#     auth_repository,
#     persisted_user,
# ):
#     user = await auth_repository.authenticate(
#         persisted_user.email,
#         "wrong-password",
#     )

#     assert user is None


# async def test_authenticate_returns_none_when_user_does_not_exist(
#     auth_repository,
# ):
#     user = await auth_repository.authenticate(
#         "missing@test.com",
#         "123456",
#     )

#     assert user is None
