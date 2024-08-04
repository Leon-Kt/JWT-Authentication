from refresh_tokens.models import RefreshToken


def get_refresh_token_object_from_db_by_user_id(user_id):
    try:
        refresh_token_object = RefreshToken.objects.get(user_id=user_id)
        print("got refresh token from db")
        return refresh_token_object
    except RefreshToken.DoesNotExist:
        print(f'Could not find refresh token for user with ID {user_id}')
    except Exception as e:
        print(f'An error occurred while retrieving refresh token: {e}')
