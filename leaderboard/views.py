from django.http import JsonResponse
from .models import Player

# Função para salvar a pontuação
def save_score(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        score = int(request.POST.get('score'))

        # Atualiza a pontuação máxima do jogador
        player, created = Player.objects.get_or_create(username=username)
        if score > player.high_score:
            player.high_score = score
            player.save()

        return JsonResponse({'status': 'success', 'high_score': player.high_score})
    return JsonResponse({'status': 'error'}, status=400)

# Função para obter os 5 melhores jogadores
def get_leaderboard(request):
    players = Player.objects.order_by('-high_score')[:5]
    leaderboard = [{'username': player.username, 'high_score': player.high_score} for player in players]
    return JsonResponse({'leaderboard': leaderboard})
