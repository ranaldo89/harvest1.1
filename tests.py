import unittest

from server import app
from flask import session
from model import connect_to_db, db, example_data, User, Recipe, Plan, PlanRecipe
import datetime

class AppTestsBasic(unittest.TestCase):
    """Basic tests for this web app."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")

    def test_homepage(self):
        """Test homepage route."""

        result = self.client.get("/")
        self.assertIn("Don't know what to eat?", result.data)


class AppTestsSignInSignOut(unittest.TestCase):
    """Test sign in and sign out."""

    def setUp(self):
        connect_to_db(app, "postgresql:///testdb")
        db.drop_all()
        self.client = app.test_client()
        app.config['TESTING'] = True
        db.create_all()
        example_data()

    def test_signin(self):
        """Test sign in route."""

        with self.client as c:
            result = c.post("/signin",
                                      data={
                                            "fname": "Bilbo",
                                            "lname": "Baggins",
                                            "email": "bilbo@gmail.com",
                                            "bday": "2000-01-01 00:00:00",
                                            "gender": "m",
                                            "pw": "bilbo"
                                            },
                                      follow_redirects=True
                                      )
            self.assertIn("Hello, Bilbo", result.data)
            self.assertIn("My Meals", result.data)
            self.assertEqual(session["user_id"], 1)


    def test_signout(self):
        """Test sign out route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get("/signout", follow_redirects=True)
            self.assertIn("Don't know what to eat?", result.data)
            self.assertNotIn('user_id', session)


class AppTestsDatabase(unittest.TestCase):
    """Tests that use the database."""

    def setUp(self):
        connect_to_db(app, "postgresql:///testdb")
        db.drop_all()
        self.client = app.test_client()
        app.config['TESTING'] = True
        db.create_all()
        example_data()

        def _mock_check_password_hash(user_pw, pw):
            return True

        import server
        server.check_password_hash = _mock_check_password_hash

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_create_account(self):
        """Test create account route."""

        with self.client as c:
            result = c.post("/new-account",
                                      data={
                                            "fname": "Frodo",
                                            "lname": "Baggins",
                                            "email": "frodo@gmail.com",
                                            "bday": "2000-05-05 00:00:00",
                                            "gender": "m",
                                            "pw": "frodo",
                                            "confirm_pw": "frodo"
                                            },
                                      follow_redirects=True
                                      )
            self.assertIn("Hello, Frodo", result.data)
            self.assertIn("no meal plans yet", result.data)
            self.assertEqual(session["user_id"], 2)

    def test_check_email(self):
        """Test check for email in db."""

        result = self.client.get("/emails-from-db", data={"email": "harry@gmail.com"},
                                          follow_redirects=True)
        self.assertIn("true", result.data)

        # result2 = self.client.get("/emails-from-db", data={"email": "bilbo@gmail.com"},
        #                                   follow_redirects=True)
        # self.assertIn("false", result2.data)

    def test_check_credentials(self):
        """Test check if users credentials are valid."""

        # check for non-unique email
        result = self.client.get("/check-credentials", data={
            "email": "bilbo@gmail.com",
            "pw": "bilbo"
            })
        self.assertIn("false", result.data)

        # check for matching pw
        # result2 = self.client.get("/check-credentials", data={
        #     "email": "harry@gmail.com",
        #     "pw": "harry"
        #     })
        # self.assertIn("true", result2.data)


class AppTestsSavedRecipe(unittest.TestCase):
    """Tests that use the saved recipes."""

    def setUp(self):
        connect_to_db(app, "postgresql:///testdb")
        db.drop_all()
        self.client = app.test_client()
        app.config['TESTING'] = True
        db.create_all()
        example_data()

    def test_saved_recipes(self):
        """Test saved-recipes route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

        result = self.client.post("/save-recipes", data={"start": datetime.date(2018, 4, 30),
                                                         "recipe-1": '{"protein":14.42,"carbs":8.78,"fat":40.32,"prepTime":20,"image":"https://spoonacular.com/recipeImages/479101-556x370.jpg","url":"http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/","title":"On the Job: Pan Roasted Cauliflower From Food52","id":479101}',
                                                         "recipe-2": '{"protein":14.42,"carbs":8.78,"fat":40.32,"prepTime":20,"image":"https://spoonacular.com/recipeImages/479101-556x370.jpg","url":"http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/","title":"On the Job: Pan Roasted Cauliflower From Food52","id":479101}',
                                                         "recipe-3": '{"protein":14.42,"carbs":8.78,"fat":40.32,"prepTime":20,"image":"https://spoonacular.com/recipeImages/479101-556x370.jpg","url":"http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/","title":"On the Job: Pan Roasted Cauliflower From Food52","id":479101}',
                                                         "recipe-4": '{"protein":14.42,"carbs":8.78,"fat":40.32,"prepTime":20,"image":"https://spoonacular.com/recipeImages/479101-556x370.jpg","url":"http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/","title":"On the Job: Pan Roasted Cauliflower From Food52","id":479101}',
                                                         "recipe-5": '{"protein":28.15,"carbs":23.16,"fat":11.87,"prepTime":20,"image":"https://spoonacular.com/recipeImages/604221-556x370.jpg","url":"http://damndelicious.net/2014/07/02/panda-express-chow-mein-copycat/","title":"Panda Express Chow Mein Copycat","id":604221}'},
                                                   follow_redirects=True)
        self.assertIn("On the Job: Pan Roasted Cauliflower From Food52", result.data)
        self.assertIn("Panda Express", result.data)

    def test_fat_data(self):
        """Test fat_data route to be used to create fat chart on my-meals page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['plan_id'] = '1'

            result = c.get("/fat-data.json")
            self.assertIn("Fat", result.data)

    def test_carbs_data(self):
        """Test carbs_data route to be used to create carbs chart on my-meals page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['plan_id'] = '1'

            result = c.get("/carbs-data.json")
            self.assertIn("Carbohydrates", result.data)

    def test_protein_data(self):
        """Test protein_data route to be used to create protein chart on my-meals page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['plan_id'] = '1'

            result = c.get("/protein-data.json")
            self.assertIn("Protein", result.data)

    def test_choose_rand_results(self):
        """Test choose rand results route."""
        import server

        with app.test_request_context():

            session['rec_id'] = []

            # self.maxDiff = None
            self.assertEqual(server.choose_rand_results([{
                    "id": 479102,
                    "title": "On the Job: Pan Roasted Cauliflower From Food52",
                    "readyInMinutes": 20
                }]),
                ([{
                    "id": 479102,
                    "title": "On the Job: Pan Roasted Cauliflower From Food52",
                    "readyInMinutes": 20
                }],
                0))


class AppTestsSignedOut(unittest.TestCase):
    """Tests with user signed out of session."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_profile_page(self):
        """Test that user can't see profile page when signed out."""

        result = self.client.get("/profile", follow_redirects=True)
        self.assertNotIn("Choose a cuisine", result.data)


class AppTestsSpoonacularAPI(unittest.TestCase):
    """Tests that use the Spoonacular API."""

    def setUp(self):
        connect_to_db(app, "postgresql:///testdb")
        db.drop_all()
        self.client = app.test_client()
        app.config['TESTING'] = True
        db.create_all()
        example_data()
        class O(object):
            pass
        o = O()
        i = O()

        def _mock_recipe_search(number, cuisine, exclude, intolerant):
            mock_search_results = [{
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            },{
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }
            ]

            return mock_search_results

        def _mock_nutri_search(ids):
            i.body = [{"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }, {"id": 479101,
                      "sourceUrl": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
                      "image": "https://spoonacular.com/recipeImages/479101-556x370.jpg",
                      "nutrition": {"nutrients": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]}
                    }
                    ]

            mock_nutri_results = i

            return mock_nutri_results

        def _mock_choose_rand_results(raw_results):

            mock_rand_results = ([{
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            },{
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }, {
                "id": 479101,
                "title": "On the Job: Pan Roasted Cauliflower From Food52",
                "readyInMinutes": 20
            }
            ], 100)

            return mock_rand_results

        import server
        server.make_recipe_search_request = _mock_recipe_search
        server.make_nutrition_info_request = _mock_nutri_search
        server.choose_rand_results = _mock_choose_rand_results

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_process_search(self):
        """Test results route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['rec_id'] = []

            result = c.get("/results", data=dict(
                start=datetime.date(2018, 4, 30),
                cuisine=["american"],
                exclude="",
                intolerant=""))

            self.assertIn("Pan Roasted Cauliflower From Food52", result.data)

    def test_more_results(self):
        """Test more results route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['rec_id'] = []

            result = c.get("/more-results.json", data=dict(
                start=datetime.date(2018, 4, 30),
                cuisine=["american"],
                exclude="",
                intolerant=""))

            self.assertIn("Pan Roasted Cauliflower From Food52", result.data)


class AppTestsGoogleAPI(unittest.TestCase):
    """Tests that use the Google/OAuth API."""

    def setUp(self):
        connect_to_db(app, "postgresql:///testdb")
        db.drop_all()
        self.client = app.test_client()
        app.config['TESTING'] = True
        db.create_all()
        example_data()

    def test_create_event(self):
        """Test creating a google calendar event."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['plan_id'] = '1'
                sess['credentials'] = {
                    'scopes': ['https://www.googleapis.com/auth/calendar'],
                    'token_uri': 'https://accounts.google.com/o/oauth2/token',
                    'token': 'ya29.GlynBTC-cHH6UDeFD4i1NqjG1Mo2TFVtZd5UsnLbN1ewsD8iJ5qT5u5GZl92JvM-mTaZ3RX8Ig0MYqxCAR2ubxB91RTioV_T1-l-7RkQzXGyTilpv_Re-E8qL3VuWg',
                    'client_id': '444375226281-mehunf6vdmh6dnhk116buoku41f9nu9q.apps.googleusercontent.com',
                    'client_secret': 'ZoV4Wv3K1s87Q_iaFt5zECNn',
                    'refresh_token': None}

            result = c.get("/test", follow_redirects=True)
            self.assertIn("Added to calendar!", result.data)

    def test_state(self):
        """Test the setting of state in the authorization process."""

        with self.client as c:
            result = c.get('/authorize')
            self.assertIn('state', session)

    # def test_credentials(self):
    #         """Test the setting of credentials in the authorization process."""

    #         import os
    #         os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    #         with self.client as c:
    #             with c.session_transaction() as sess:
    #                 sess['state'] = '1rcRFtKsjLSrYKcrfBcKKOl2mPMS9M'

    #             result = c.get('/oauth2callback')
    #             self.assertIn('credentials', session)

    def test_clear(self):
        """Test clearing of credentials."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['credentials'] = {
                    'scopes': ['https://www.googleapis.com/auth/calendar'],
                    'token_uri': 'https://accounts.google.com/o/oauth2/token',
                    'token': 'ya29.GlynBTC-cHH6UDeFD4i1NqjG1Mo2TFVtZd5UsnLbN1ewsD8iJ5qT5u5GZl92JvM-mTaZ3RX8Ig0MYqxCAR2ubxB91RTioV_T1-l-7RkQzXGyTilpv_Re-E8qL3VuWg',
                    'client_id': '444375226281-mehunf6vdmh6dnhk116buoku41f9nu9q.apps.googleusercontent.com',
                    'client_secret': 'ZoV4Wv3K1s87Q_iaFt5zECNn',
                    'refresh_token': None}

            result = c.get('/clear')
            self.assertNotIn('credentials', session)

if __name__ == "__main__":
    import unittest
    unittest.main()
