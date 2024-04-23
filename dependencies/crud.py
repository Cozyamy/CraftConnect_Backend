from sqlmodel import Session, select
from models.user_models import User
from utils.utils import verify_password

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user

def create_user(*, session: Session, email: str, user: User) -> User:
    user = User(email=email, first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user