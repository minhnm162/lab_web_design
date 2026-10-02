## Question 1
1. Duplicate Avengers:
   UNIQUE constraint, because team.name must be unique.

2. Ghost with team_id = 99:
   FOREIGN KEY constraint, because team 99 does not exist.

3. Hero with only age:
   NOT NULL constraint, because hero.name is required.

4. Delete team id = 1:
   FOREIGN KEY constraint, because existing heroes still reference team 1.

## Question 2

The relationship Team → Hero is one-to-many, so the foreign key is placed on the "many" side, which is Hero.

Each hero belongs to at most one team, so hero.team_id can store the id of that team. If the foreign key were placed on Team, one team would need to store many hero ids, which does not fit the relational model well.

## Question 3

To represent the many-to-many relationship between Hero and Mission, we need three tables:

1. Hero
   - id: PRIMARY KEY

2. Mission
   - id: PRIMARY KEY
   - title

3. HeroMissionLink
   - hero_id: FOREIGN KEY → Hero.id
   - mission_id: FOREIGN KEY → Mission.id
   - PRIMARY KEY (hero_id, mission_id)

## Question 4

We read DATABASE_URL from an environment variable instead of hardcoding it in database.py because:

1. Security: database credentials such as usernames and passwords should not be stored in source code or accidentally committed to Git.

2. Flexibility: different environments (development, testing, production) can use different databases without changing the Python code.

## Question 5

id is typed as int | None with default=None because a new Python object does not have an id before it is inserted into the database. The database generates the id when the row is inserted.

## Question 6

The Hero attributes that become database columns are id, name, age, secret_name, and team_id.

The team attribute created with Relationship() does not become a database column. Only team_id is stored in the table.

back_populates connects the two sides of a bidirectional relationship:
hero.team <-> team.heroes.

## Question 7

Compared with the table created manually in Part 1, the SQLModel-generated hero table has:

- An additional secret_name column, which is NOT NULL.
- An index on name: ix_hero_name.
- id is generated automatically using a sequence/SERIAL and is the primary key.
- name is NOT NULL.
- age and team_id are nullable.
- team_id still has a foreign key referencing team(id).

The PostgreSQL output may display VARCHAR as "character varying", but they represent the same type.

## Question 8

No. After restarting the server, CREATE TABLE is not executed again for existing tables.

SQLModel.metadata.create_all(engine) creates tables that do not exist, but it does not recreate or alter tables that already exist.

## Question 9

The line:

from app import models

imports the table models so that Hero and Team are registered in SQLModel.metadata before create_all() runs.

## Question 10

If `session.commit()` is commented out, the new hero is not permanently saved in the database.

`session.add(hero)` only adds the object to the current SQLAlchemy session. It does not permanently save the transaction.

Because the code still calls `session.refresh(hero)`, the request may fail because the object has not been committed yet.

The row is not permanently stored in PostgreSQL.

We need `session.commit()` to save the transaction permanently.

We use `session.refresh(hero)` after the commit to reload the object from the database and obtain database-generated values such as the new `id`.

## Question 11

For a PATCH request with:

```json
{
  "age": 17
}
```

SQLAlchemy prints an UPDATE statement similar to:

```sql
UPDATE hero
SET age = %(age)s
WHERE hero.id = %(hero_id)s;
```

It updates only the `age` column, not every column.

This happens because the code uses:

```python
hero_in.model_dump(exclude_unset=True)
```

so only the fields actually sent by the client are included in the update.

## Question 12

No, `secret_name` is not included in the JSON returned by:

```text
GET /heroes/{id}
```

The line responsible for this is:

```python
response_model=HeroPublic
```

`HeroPublic` does not contain the `secret_name` field, so FastAPI filters it out of the response before sending the JSON back to the client.


## Question 13

For GET /heroes?min_age=18&team_id=1, the SQL printed by echo=True uses bound parameters instead of inserting the values directly into the SQL string.

The values 18 and 1 are passed separately as query parameters.

This is safer against SQL injection because SQLAlchemy sends the SQL structure and the parameter values separately instead of concatenating user input into raw SQL.

## Question 14

Filtering in the database is better because the database only returns the rows we need.

If we load all heroes into Python first and then filter them, it wastes memory, transfers unnecessary data, and becomes slower when the table is large.

## Question 15

create_all() creates database tables that do not already exist.

On restart, it created mission and heromissionlink because they were new tables.

It did not recreate hero because the hero table already existed.

create_all() creates missing tables, but it does not recreate or modify existing tables.

## Question 16

The Team rows are inserted before the Hero rows.

Because the Hero objects were created with relationships such as
team=avengers instead of manually setting team_id, SQLModel/SQLAlchemy
first inserts the Team, obtains its generated id, and then uses that id
as hero.team_id when inserting the Hero rows.

The link-table rows are also created automatically from the missions
relationships.


## Question 18

upgrade() adds the nullable power column to the hero table.

downgrade() removes the power column from the hero table.

## Question 19

Alembic stores the current database revision in the alembic_version table.

The migrations/ folder should be committed to Git so that every developer
and deployment environment can apply the same schema changes in the same order.

## Question 20

Alembic interpreted the rename as removing the old secret_name column and
adding a new alias column.

This is dangerous because dropping secret_name could delete all existing
data stored in that column.

Instead, the migration should be edited manually to rename the existing
column, for example by using op.alter_column(..., new_column_name="alias").

The test migration should not be applied. After reviewing it, delete the
revision file and change alias back to secret_name in the model.