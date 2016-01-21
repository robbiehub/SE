import unittest
import recommendations

class TestRecommendations(unittest.TestCase):

    def test_DistEuclidiana(self):
        self.assertEqual(recommendations.sim_distance(recommendations.critics, 'Lisa Rose','Gene Seymour'), 0.14814814814814814)

    def test_Pearson(self):
        self.assertEqual(recommendations.sim_pearson(recommendations.critics, 'Lisa Rose','Gene Seymour'), 0.39605901719066977)

    def test_TopMatches(self):
        self.assertEqual(recommendations.topMatches(recommendations.critics,'Toby',n=1)[0],(0.99124070716192991, 'Lisa Rose'))

    def test_getRecommendations(self):
        self.assertEqual(recommendations.getRecommendations(recommendations.critics,'Toby')[0],(3.3477895267131013, 'The Night Listener'))

    def test_transformPrefs(self):
        self.assertEqual(recommendations.transformPrefs(recommendations.critics)['Lady in the Water'],
                        {'Lisa Rose': 2.5, 'Jack Matthews': 3.0, 'Michael Phillips': 2.5, 'Gene Seymour': 3.0, 'Mick LaSalle': 3.0})

    def test_calculateSimilarItems(self):
        self.assertEqual(recommendations.calculateSimilarItems(recommendations.critics)['Lady in the Water'], [(0.4, 'You, Me and Dupree'), (0.2857142857142857, 'The Night Listener'), (0.2222222222222222, 'Snakes on a Plane'), (0.2222222222222222, 'Just My Luck'), (0.09090909090909091, 'Superman Returns')])

    def test_getRecommendedItems(self):
        self.assertEqual(recommendations.getRecommendedItems(recommendations.critics, recommendations.calculateSimilarItems(recommendations.critics),'Toby'),
                        [(3.182634730538922, 'The Night Listener'),(2.5983318700614575, 'Just My Luck'),(2.4730878186968837, 'Lady in the Water')])

if __name__ == "__main__":
    unittest.main()
