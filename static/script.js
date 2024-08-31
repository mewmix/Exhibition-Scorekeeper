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
                console.log("Match ID selected:", matchId); // Debug log

                // Set match_id in hidden input
                const matchIdInput = document.getElementById('match_id');
                if (matchIdInput) {
                    matchIdInput.value = matchId;
                    console.log("Match ID set in hidden input:", matchIdInput.value); // Debug log
                }

                // Update the game action form
                fetch(`/game_action_form/${matchId}`)
                    .then(response => response.text())
                    .then(html => {
                        document.getElementById('game_action_form').innerHTML = html;

                        // Ensure hidden input is set after form update
                        const updatedMatchIdInput = document.getElementById('match_id');
                        if (updatedMatchIdInput) {
                            updatedMatchIdInput.value = matchId;
                            console.log("Match ID re-set after form update:", updatedMatchIdInput.value); // Debug log
                        }

                        // Re-attach event listener for form submission after updating the form
                        attachFormSubmissionListener();
                    });

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
                    });

                // Update the stats button data attribute
                const statsButton = document.getElementById('load-stats-btn');
                if (statsButton) {
                    statsButton.setAttribute('data-match-id', matchId);
                }
            }
        }
    });

    // Function to attach form submission event listener
    function attachFormSubmissionListener() {
        // Handle the form submission with fetch for game actions
        const form = document.getElementById('game-action-form');
        if (form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();

                const formData = new FormData(form);

                // Ensure the match_id is added to the formData
                const matchId = document.getElementById('match_id').value;
                console.log("Form data before submission:", Array.from(formData.entries())); // Debug log

                if (!formData.has('match_id')) {
                    formData.append('match_id', matchId);
                }
                console.log("Form data with match_id:", Array.from(formData.entries())); // Debug log

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
        }
    }

    // Initial attachment of the form submission listener
    attachFormSubmissionListener();

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
});
