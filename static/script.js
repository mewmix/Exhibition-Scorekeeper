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
    document.getElementById('load-stats-btn').addEventListener('click', function() {
        // Retrieve the match ID from the data attribute
        const matchId = this.getAttribute('data-match-id');
        if (matchId) {
            // Construct the URL using the match ID
            const statsUrl = `/game/stats/${matchId}`;
    
            fetch(statsUrl)
                .then(response => response.json())
                .then(data => {
                    const statsContainer = document.getElementById('game-stats-content');
                    statsContainer.innerHTML = `
                        <p><strong>Game:</strong> ${data.game}</p>
                        <p><strong>Player 1:</strong> ${data.player1_name}</p>
                        <p><strong>Player 2:</strong> ${data.player2_name}</p>
                        <p><strong>Lag Winner:</strong> ${data.lag_winner ? data.lag_winner : 'None'}</p>
                        <p><strong>Break Shot Taken:</strong> ${data.break_shot_taken}</p>
                        <p><strong>Break and Run:</strong> ${data.break_and_run}</p>
                        <p><strong>Current Shooter:</strong> ${data.current_shooter ? data.current_shooter : 'None'}</p>
                        <p><strong>Inning Total:</strong> ${data.inning_total}</p>
                        <p><strong>Eightball Rack Count:</strong> ${data.eightball_rack_count}</p>
                        <p><strong>Match Start:</strong> ${data.match_start_human_readable}</p>
                        <p><strong>Game Log:</strong></p>
                        <ul class="game-log">
                            ${Object.entries(data.game_log).map(([key, value]) => `<li>${value}</li>`).join('')}
                        </ul>
                    `;
                })
                .catch(error => {
                    console.error('Error fetching game stats:', error);
                    document.getElementById('game-stats-content').innerHTML = '<p>Error loading stats. Please try again.</p>';
                });
        } else {
            console.error('Match ID not found.');
        }
    });
    document.addEventListener("DOMContentLoaded", function() {
        // Assuming matchId is defined somewhere in your JavaScript, possibly passed from the server or another script
        const matchId = 1; // Replace with dynamic value if needed
    
        // Function to update the rack based on the game state
        function updateRack(gameState) {
            // Clear all pocketed states
            document.querySelectorAll(".ball").forEach(function(ball) {
                ball.classList.remove("pocketed");
            });
    
            // Mark pocketed balls
            const pocketedBalls = gameState.player1_balls_pocketed.concat(gameState.player2_balls_pocketed);
            pocketedBalls.forEach(function(ball) {
                const ballElement = document.querySelector(`.ball[data-ball="${ball}"]`);
                if (ballElement) {
                    ballElement.classList.add("pocketed");
                }
            });
        }
    
        // Fetch the current game state when the page loads
        function fetchGameState() {
            fetch(`/game/stats/${matchId}`)  // Use backticks to properly interpolate matchId
            .then(response => response.json())
            .then(data => updateRack(data))
            .catch(error => console.error("Error fetching game state:", error));
        }
    
        // Initial fetch to update the rack on page load
        fetchGameState();
    });
    
});
