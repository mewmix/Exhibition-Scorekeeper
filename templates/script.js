
document.addEventListener('DOMContentLoaded', function() {
    // Fetch and populate current matches on load
    fetch('/current_matches')
        .then(response => response.text())
        .then(html => {
            document.getElementById('matches_container').innerHTML = html;
        });

    // Handle change event for match selection
    document.body.addEventListener('change', function(event) {
        if (event.target && event.target.id === 'current_match_select') {
            var matchId = event.target.value;
            if (matchId) {
                // Update the game action form
                fetch(`/game_action_form/${matchId}`)
                    .then(response => response.text())
                    .then(html => {
                        document.getElementById('game_action_form').innerHTML = html;
                    });

                // Fetch players for lag_to_break action
                fetch(`/get_players/${matchId}`)
                    .then(response => response.json())
                    .then(data => {
                        const lagWinnerSelect = document.getElementById('lag_winner');
                        lagWinnerSelect.innerHTML = `
                            <option value="${data.player1_name}">${data.player1_name}</option>
                            <option value="${data.player2_name}">${data.player2_name}</option>
                        `;
                    });

                // Update the stats button data attribute
                document.getElementById('load-stats-btn').setAttribute('data-match-id', matchId);
            }
        }
    });

    // Handle click event for loading game stats
    document.getElementById('load-stats-btn').addEventListener('click', function() {
        var matchId = this.getAttribute('data-match-id');
        if (matchId) {
            var statsUrl = `/game/stats/${matchId}`;
            fetch(statsUrl)
                .then(response => response.json())
                .then(data => {
                    var statsDiv = document.getElementById('stats');
                    statsDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                });
        }
    });

    // Handle the form submission with fetch for game actions
    document.getElementById('game-action-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        fetch('/game/action', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('action-response').innerHTML = `<p>${data.message || data.error}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
