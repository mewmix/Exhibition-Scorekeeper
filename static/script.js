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
            const matchId = event.target.value;
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

                // Fetch and update the game state (rack and stats)
                fetchGameState(matchId);
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
                    if (data.current_game_state) {
                        updateRack(data.current_game_state);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        }
    }

    // Function to fetch the game state and update the rack
    function fetchGameState(matchId) {
        fetch(`/game/stats/${matchId}`)
            .then(response => response.json())
            .then(data => {
                updateRack(data);
                updateStats(data);
            })
            .catch(error => console.error("Error fetching game state:", error));
    }

    // Function to update the rack based on the game state
    function updateRack(gameState) {
        document.querySelectorAll(".ball").forEach(function(ball) {
            ball.classList.remove("pocketed");
        });

        const pocketedBalls = gameState.player1_balls_pocketed.concat(gameState.player2_balls_pocketed);
        pocketedBalls.forEach(function(ball) {
            const ballElement = document.querySelector(`.ball[data-ball="${ball}"]`);
            if (ballElement) {
                ballElement.classList.add("pocketed");
            }
        });

        // Attach event listeners to each ball to handle pocketing or break shot
        document.querySelectorAll(".ball").forEach(function(ball) {
            ball.addEventListener("click", function() {
                const ballNumber = this.getAttribute("data-ball");
                if (!this.classList.contains("pocketed")) {
                    const actionType = document.querySelector('input[name="action_type"]:checked').value;
                    submitBallAction(matchId, ballNumber, actionType);
                }
            });
        });
    }

    // Function to update the game stats
    function updateStats(gameState) {
        const statsContainer = document.getElementById('game-stats-content');
        statsContainer.innerHTML = `
            <p><strong>Game Type:</strong> ${gameState.game_type}</p>
            <p><strong>Player 1:</strong> ${gameState.player1_name}</p>
            <p><strong>Player 2:</strong> ${gameState.player2_name}</p>
            <p><strong>Lag Winner:</strong> ${gameState.lag_winner || 'None'}</p>
            <p><strong>Break Shot Taken:</strong> ${gameState.break_shot_taken ? 'Yes' : 'No'}</p>
            <p><strong>Break and Run:</strong> ${gameState.break_and_run ? 'Yes' : 'No'}</p>
            <p><strong>Current Shooter:</strong> ${gameState.current_shooter || 'None'}</p>
            <p><strong>Inning Total:</strong> ${gameState.inning_total}</p>
            <p><strong>Eightball Rack Count:</strong> ${gameState.eightball_rack_count}</p>
            <p><strong>Match Start:</strong> ${gameState.match_start_human_readable}</p>
            <p><strong>Game Log:</strong></p>
            <ul class="game-log">
                ${Object.entries(gameState.game_log).map(([key, value]) => `<li>${value}</li>`).join('')}
            </ul>
        `;
    }

    // Function to submit a ball action (pocket or break shot)
    function submitBallAction(matchId, ballNumber, actionType) {
        const formData = new FormData();
        formData.append('match_id', matchId);
        formData.append('action', actionType);
        formData.append('ball_number', ballNumber);

        fetch('/game/action', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Action processed successfully") {
                updateRack(data.current_game_state);
                updateStats(data.current_game_state);
            } else {
                alert(data.error || "Failed to process the action.");
            }
        })
        .catch(error => console.error("Error processing action:", error));
    }

    // Initial attachment of the form submission listener
    attachFormSubmissionListener();

    // Event listener for the stats button to load game stats
    document.getElementById('load-stats-btn').addEventListener('click', function() {
        const matchId = this.getAttribute('data-match-id');
        if (matchId) {
            fetchGameState(matchId);
        } else {
            console.error('Match ID not found.');
        }
    });

    // Function to handle page load initial state
    function initializePage() {
        const matchIdInput = document.getElementById('match_id');
        if (matchIdInput && matchIdInput.value) {
            fetchGameState(matchIdInput.value);
        }
    }

    // Initialize the page on load
    initializePage();
});
