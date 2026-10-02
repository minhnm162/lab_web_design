from sqlmodel import Session, SQLModel, select

from app.database import engine
from app.models import Hero, Mission, Team


def seed():
    # Tạo các table còn thiếu
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        # Nếu đã có ít nhất 1 team thì dừng
        existing_team = session.exec(
            select(Team)
        ).first()

        if existing_team:
            print("Database already seeded")
            return

        # TEAMS
        avengers = Team(
            name="Avengers",
            headquarters="New York"
        )

        xmen = Team(
            name="X-Men",
            headquarters="Westchester"
        )

        # MISSIONS

        sokovia = Mission(
            title="Battle of Sokovia"
        )

        save_world = Mission(
            title="Save the World"
        )

        # HEROES

        tony = Hero(
            name="Tony",
            age=45,
            secret_name="Iron Man",
            team=avengers,
            missions=[sokovia]
        )

        natasha = Hero(
            name="Natasha",
            age=35,
            secret_name="Black Widow",
            team=avengers,
            missions=[sokovia, save_world]
        )

        steve = Hero(
            name="Steve",
            age=40,
            secret_name="Captain America",
            team=avengers,
            missions=[save_world]
        )

        logan = Hero(
            name="Logan",
            age=150,
            secret_name="Wolverine",
            team=xmen,
            missions=[save_world]
        )

        peter = Hero(
            name="Peter",
            age=16,
            secret_name="Spider-Man",
            team=avengers
        )

        # Chỉ cần add các object chính.
        # SQLModel sẽ xử lý relationships.
        session.add(avengers)
        session.add(xmen)
        session.add(sokovia)
        session.add(save_world)

        session.add(tony)
        session.add(natasha)
        session.add(steve)
        session.add(logan)
        session.add(peter)

        session.commit()

        print("Database seeded successfully")


if __name__ == "__main__":
    seed()