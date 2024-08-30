document.addEventListener('DOMContentLoaded', function() {
    // Fetch and populate current matches on load
    fetch('/current_matches')
        .then(response => response.text())
        .then(html => {
            document.getElementById('matches_container').innerHTML = html;
        })
        .catch(error => console.error('Error loading matches:', error));

    // Handle change event for match selection
    document.body.addEventListener('change', function(event) {
        if (event.target && event.target.id === 'current_match_select') {
            var matchId = event.target.value;
            if (matchId) {
                // Update the game action form
                fetch(`/game_action_form/${matchId}`)
                    .then(response => response.text())
                    .then(html => {
                        const formContainer = document.getElementById('game_action_form');
                        if (formContainer) {
                            formContainer.innerHTML = html;
                        }
                    })
                    .catch(error => console.error('Error loading action form:', error));

                // Fetch players for lag_to_break action
                fetch(`/get_players/${matchId}`)
                    .then(response => response.json())
                    .then(data => {
                        const lagWinnerSelect = document.getElementById('lag_winner');
                        if (lagWinnerSelect) {
                            lagWinnerSelect.innerHTML = `
                                <option value="${data.player1_name}">${data.player1_name}</option>
                                <option value="${data.player2_name}">${data.player2_name}</option>
                            `;
                        }
                    })
                    .catch(error => console.error('Error loading players:', error));

                // Update the stats button data attribute
                const loadStatsBtn = document.getElementById('load-stats-btn');
                if (loadStatsBtn) {
                    loadStatsBtn.setAttribute('hx-get', `/game/stats/${matchId}`);
                }
            }
        }
    });
    // Handle the form submission with fetch for game actions
    const gameActionForm = document.getElementById('game-action-form');
    if (gameActionForm) {
        gameActionForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(gameActionForm);

            fetch('/game/action', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                const actionResponse = document.getElementById('action-response');
                if (actionResponse) {
                    actionResponse.innerHTML = `<p>${data.message || data.error}</p>`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
