from django.test import TestCase
from .models import Score

class ScoreModelTest(TestCase):

    def setUp(self):
        """Método para preparar dados antes de cada teste"""
        self.score = Score.objects.create(
            name="Jogador1",
            score=1000,
            time=50.5
        )

    def test_score_creation(self):
        """Teste para verificar se o modelo Score foi criado corretamente"""
        self.assertEqual(self.score.name, "Jogador1")
        self.assertEqual(self.score.score, 1000)
        self.assertEqual(self.score.time, 50.5)

    def test_str_method(self):
        """Teste para verificar se o método __str__ retorna o valor correto"""
        self.assertEqual(str(self.score), "Jogador1 - 1000 pontos - 50.5 segundos")

class ScoreViewTest(TestCase):

    def setUp(self):
        """Método para preparar dados antes de cada teste"""
        self.score = Score.objects.create(
            name="Jogador1",
            score=1000,
            time=50.5
        )

    def test_score_view(self):
        """Teste para verificar se a página de ranking retorna status 200"""
        response = self.client.get('/leaderboard/')  # Supondo que você tenha uma URL de ranking
        self.assertEqual(response.status_code, 200)
