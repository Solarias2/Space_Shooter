def load_leaderboard():
    leaderboard = []
    with open('leaderboard.txt', 'r') as file:
        for line in file:
            name, score = line.strip().split(',')
            leaderboard.append((name, int(score)))
    return leaderboard

def save_leaderboard(leaderboard):
    with open('leaderboard.txt', 'w') as file:
        for entry in leaderboard:
            name, score = entry
            file.write(f"{name},{score}\n")

def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append((name, score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)  # Sort scores in descending order
    leaderboard = leaderboard[:10]  # Keep only the top 10 scores
    save_leaderboard(leaderboard)