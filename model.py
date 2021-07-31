"""Models and database functions"""
from flask_sqlalchemy import SQLAlchemy
import datetime

# connection to the PostgreSQL database
db = SQLAlchemy()

############################## Model definitions ###############################


class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pw = db.Column(db.String(100), nullable=False)
    bday = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} fname={} lname={}>".format(self.user_id, self.fname, self.lname)


class Recipe(db.Model):
    """Saved recipe on website (from Spoonacular API)."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    num_saved = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_id={} title={} num_saved={}>".format(self.recipe_id, self.title, self.num_saved)


class Plan(db.Model):
    """Saved meal plans on website."""

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    start = db.Column(db.Date, nullable=False)

    recipes = db.relationship("Recipe", secondary="assoc", backref="plans")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Plan plan_id={} user_id={} start={}>".format(self.plan_id, self.user_id, self.start)


class PlanRecipe(db.Model):
    """User of website."""

    __tablename__ = "assoc"

    assoc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), index=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Assoc assoc_id={} user_id={} recipe_id={}>".format(self.assoc_id, self.user_id, self.recipe_id)


############################## Helper Functions ###############################

def example_data():
    user = User(fname="Bilbo",
                lname="Baggins",
                email="bilbo@gmail.com",
                pw="bilbo",
                bday="2000-01-01 00:00:00",
                gender="m"
                )
    plan = Plan(user_id=1,
                start=datetime.date(2015, 5, 23))
    recipe1 = Recipe(recipe_id=479101,
                    num_saved=1,
                    title="On the Job: Pan Roasted Cauliflower From Food52",
                    url="http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                    image="https://spoonacular.com/recipeImages/479101-556x370.jpg",
                    prep_time=20,
                    fat=40.32,
                    carbohydrates=8.78,
                    protein=14.42
                    )
    recipe2 = Recipe(recipe_id=479102,
                    num_saved=1,
                    title="On the Job: Pan Roasted Cauliflower From Food52",
                    url="http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                    image="https://spoonacular.com/recipeImages/479101-556x370.jpg",
                    prep_time=20,
                    fat=40.32,
                    carbohydrates=8.78,
                    protein=14.42
                    )
    recipe3 = Recipe(recipe_id=479103,
                    num_saved=1,
                    title="On the Job: Pan Roasted Cauliflower From Food52",
                    url="http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                    image="https://spoonacular.com/recipeImages/479101-556x370.jpg",
                    prep_time=20,
                    fat=40.32,
                    carbohydrates=8.78,
                    protein=14.42
                    )
    recipe4 = Recipe(recipe_id=479104,
                    num_saved=1,
                    title="On the Job: Pan Roasted Cauliflower From Food52",
                    url="http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                    image="https://spoonacular.com/recipeImages/479101-556x370.jpg",
                    prep_time=20,
                    fat=40.32,
                    carbohydrates=8.78,
                    protein=14.42
                    )
    recipe5 = Recipe(recipe_id=479105,
                    num_saved=1,
                    title="On the Job: Pan Roasted Cauliflower From Food52",
                    url="http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                    image="https://spoonacular.com/recipeImages/479101-556x370.jpg",
                    prep_time=20,
                    fat=40.32,
                    carbohydrates=8.78,
                    protein=14.42
                    )                                          


    db.session.add(user)
    db.session.add(plan)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.add(recipe3)
    db.session.add(recipe4)
    db.session.add(recipe5)
    db.session.commit()


def connect_to_db(app, db_uri='postgresql://postgres:00000@localhost/harvest'):
    

    """Connect the database to the Flask app."""
   
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from app import app
    connect_to_db(app)
    db.create_all()
    print ("Connected to DB")
