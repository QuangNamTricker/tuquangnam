document.addEventListener('DOMContentLoaded', function() {
    // Play startup sound
    const startupSound = document.getElementById('startup-sound');
    const clickSound = document.getElementById('click-sound');
    startupSound.play();
    
    // Update clock
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        document.getElementById('clock').textContent = timeString;
    }
    
    setInterval(updateClock, 1000);
    updateClock();
    
    // Window management
    let activeWindow = null;
    let zIndex = 100;
    
    function openApp(appId) {
        // Play click sound
        clickSound.currentTime = 0;
        clickSound.play();
        
        // Close current active window if it's the same app
        if (activeWindow && activeWindow.id === `${appId}-window`) {
            closeActiveWindow();
            return;
        }
        
        // Close current active window
        if (activeWindow) {
            activeWindow.classList.remove('active');
            const taskbarIcon = document.querySelector(`.taskbar-icon[data-app="${activeWindow.id.replace('-window', '')}"]`);
            if (taskbarIcon) {
                taskbarIcon.classList.remove('active');
            }
        }
        
        // Open new window
        const window = document.getElementById(`${appId}-window`);
        if (window) {
            window.classList.add('active');
            window.style.zIndex = zIndex++;
            activeWindow = window;
            
            // Position window if it's the first time opening
            if (!window.dataset.positioned) {
                window.style.left = `${Math.random() * (window.parentElement.clientWidth - window.offsetWidth)}px`;
                window.style.top = `${Math.random() * (window.parentElement.clientHeight - window.offsetHeight)}px`;
                window.dataset.positioned = 'true';
            }
            
            // Update taskbar
            const taskbarIcon = document.querySelector(`.taskbar-icon[data-app="${appId}"]`);
            if (taskbarIcon) {
                taskbarIcon.classList.add('active');
            }
        }
    }
    
    function closeActiveWindow() {
        if (activeWindow) {
            activeWindow.classList.remove('active');
            const appId = activeWindow.id.replace('-window', '');
            const taskbarIcon = document.querySelector(`.taskbar-icon[data-app="${appId}"]`);
            if (taskbarIcon) {
                taskbarIcon.classList.remove('active');
            }
            activeWindow = null;
        }
    }
    
    // Desktop icons
    document.querySelectorAll('.icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const appId = this.dataset.app;
            openApp(appId);
        });
    });
    
    // Taskbar icons
    document.querySelectorAll('.taskbar-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const appId = this.dataset.app;
            openApp(appId);
        });
    });
    
    // Window controls
    document.querySelectorAll('.window .close').forEach(button => {
        button.addEventListener('click', closeActiveWindow);
    });
    
    document.querySelectorAll('.window .minimize').forEach(button => {
        button.addEventListener('click', function() {
            if (activeWindow) {
                activeWindow.classList.remove('active');
                const appId = activeWindow.id.replace('-window', '');
                const taskbarIcon = document.querySelector(`.taskbar-icon[data-app="${appId}"]`);
                if (taskbarIcon) {
                    taskbarIcon.classList.remove('active');
                }
                activeWindow = null;
            }
        });
    });
    
    // Make windows draggable
    document.querySelectorAll('.window .title-bar').forEach(titleBar => {
        titleBar.addEventListener('mousedown', function(e) {
            const window = this.closest('.window');
            window.style.zIndex = zIndex++;
            activeWindow = window;
            
            // Update taskbar
            document.querySelectorAll('.taskbar-icon').forEach(icon => {
                icon.classList.remove('active');
            });
            const appId = window.id.replace('-window', '');
            const taskbarIcon = document.querySelector(`.taskbar-icon[data-app="${appId}"]`);
            if (taskbarIcon) {
                taskbarIcon.classList.add('active');
            }
            
            let shiftX = e.clientX - window.getBoundingClientRect().left;
            let shiftY = e.clientY - window.getBoundingClientRect().top;
            
            function moveAt(pageX, pageY) {
                const desktop = document.querySelector('.desktop');
                const desktopRect = desktop.getBoundingClientRect();
                
                let left = pageX - shiftX - desktopRect.left;
                let top = pageY - shiftY - desktopRect.top;
                
                // Boundary checks
                if (left < 0) left = 0;
                if (top < 0) top = 0;
                if (left + window.offsetWidth > desktopRect.width) {
                    left = desktopRect.width - window.offsetWidth;
                }
                if (top + window.offsetHeight > desktopRect.height) {
                    top = desktopRect.height - window.offsetHeight;
                }
                
                window.style.left = left + 'px';
                window.style.top = top + 'px';
            }
            
            function onMouseMove(e) {
                moveAt(e.pageX, e.pageY);
            }
            
            document.addEventListener('mousemove', onMouseMove);
            
            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
            }
            
            document.addEventListener('mouseup', onMouseUp);
        });
    });
    
    // Notepad functionality
    const notepadContent = document.getElementById('notepad-content');
    if (localStorage.getItem('notepadContent')) {
        notepadContent.value = localStorage.getItem('notepadContent');
    }
    
    notepadContent.addEventListener('input', function() {
        localStorage.setItem('notepadContent', this.value);
    });
    
    // Calculator functionality
    const calculatorDisplay = document.getElementById('calculator-display');
    let calculatorValue = '';
    
    document.querySelectorAll('.calculator button').forEach(button => {
        button.addEventListener('click', function() {
            clickSound.currentTime = 0;
            clickSound.play();
            
            const value = this.textContent;
            
            if (value === 'C') {
                calculatorValue = '';
            } else if (value === '=') {
                try {
                    calculatorValue = eval(calculatorValue).toString();
                } catch (e) {
                    calculatorValue = 'Error';
                }
            } else {
                calculatorValue += value;
            }
            
            calculatorDisplay.value = calculatorValue;
        });
    });
    
    // Paint functionality
    const paintCanvas = document.getElementById('paint-canvas');
    const paintCtx = paintCanvas.getContext('2d');
    let isDrawing = false;
    
    // Set canvas size
    function resizeCanvas() {
        paintCanvas.width = paintCanvas.parentElement.clientWidth - 10;
        paintCanvas.height = paintCanvas.parentElement.clientHeight - 50;
        paintCtx.fillStyle = 'white';
        paintCtx.fillRect(0, 0, paintCanvas.width, paintCanvas.height);
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Drawing tools
    let currentTool = 'pencil';
    let currentColor = '#000000';
    let brushSize = 5;
    
    document.querySelectorAll('[data-tool]').forEach(tool => {
        tool.addEventListener('click', function() {
            currentTool = this.dataset.tool;
        });
    });
    
    document.getElementById('paint-color').addEventListener('input', function() {
        currentColor = this.value;
    });
    
    document.getElementById('brush-size').addEventListener('input', function() {
        brushSize = this.value;
    });
    
    // Drawing functions
    paintCanvas.addEventListener('mousedown', startDrawing);
    paintCanvas.addEventListener('mousemove', draw);
    paintCanvas.addEventListener('mouseup', stopDrawing);
    paintCanvas.addEventListener('mouseout', stopDrawing);
    
    function startDrawing(e) {
        isDrawing = true;
        draw(e);
    }
    
    function draw(e) {
        if (!isDrawing) return;
        
        const rect = paintCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        paintCtx.lineWidth = brushSize;
        paintCtx.lineCap = 'round';
        
        if (currentTool === 'pencil') {
            paintCtx.strokeStyle = currentColor;
            paintCtx.lineTo(x, y);
            paintCtx.stroke();
            paintCtx.beginPath();
            paintCtx.moveTo(x, y);
        } else if (currentTool === 'eraser') {
            paintCtx.strokeStyle = 'white';
            paintCtx.lineTo(x, y);
            paintCtx.stroke();
            paintCtx.beginPath();
            paintCtx.moveTo(x, y);
        }
    }
    
    function stopDrawing() {
        isDrawing = false;
        paintCtx.beginPath();
    }
    
    // Snake Game (Easter Egg)
    const gameCanvas = document.getElementById('game-canvas');
    const gameCtx = gameCanvas.getContext('2d');
    let snake = [];
    let food = {};
    let direction = 'right';
    let gameLoop;
    let score = 0;
    
    function initGame() {
        snake = [
            {x: 150, y: 150},
            {x: 140, y: 150},
            {x: 130, y: 150},
            {x: 120, y: 150},
            {x: 110, y: 150}
        ];
        
        generateFood();
        direction = 'right';
        score = 0;
        document.getElementById('game-score').textContent = `Score: ${score}`;
        
        if (gameLoop) clearInterval(gameLoop);
        gameLoop = setInterval(updateGame, 100);
    }
    
    function generateFood() {
        food = {
            x: Math.floor(Math.random() * 30) * 10,
            y: Math.floor(Math.random() * 30) * 10
        };
        
        // Make sure food doesn't appear on snake
        for (let segment of snake) {
            if (segment.x === food.x && segment.y === food.y) {
                return generateFood();
            }
        }
    }
    
    function updateGame() {
        // Move snake
        const head = {x: snake[0].x, y: snake[0].y};
        
        switch (direction) {
            case 'up':
                head.y -= 10;
                break;
            case 'down':
                head.y += 10;
                break;
            case 'left':
                head.x -= 10;
                break;
            case 'right':
                head.x += 10;
                break;
        }
        
        // Check collision with walls
        if (head.x < 0 || head.x >= gameCanvas.width || head.y < 0 || head.y >= gameCanvas.height) {
            gameOver();
            return;
        }
        
        // Check collision with self
        for (let segment of snake) {
            if (segment.x === head.x && segment.y === head.y) {
                gameOver();
                return;
            }
        }
        
        // Check if snake ate food
        if (head.x === food.x && head.y === food.y) {
            score += 10;
            document.getElementById('game-score').textContent = `Score: ${score}`;
            generateFood();
        } else {
            snake.pop();
        }
        
        snake.unshift(head);
        
        // Draw everything
        drawGame();
    }
    
    function drawGame() {
        // Clear canvas
        gameCtx.fillStyle = 'black';
        gameCtx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        // Draw snake
        snake.forEach((segment, index) => {
            gameCtx.fillStyle = index === 0 ? 'lime' : 'green';
            gameCtx.fillRect(segment.x, segment.y, 10, 10);
            gameCtx.strokeStyle = 'darkgreen';
            gameCtx.strokeRect(segment.x, segment.y, 10, 10);
        });
        
        // Draw food
        gameCtx.fillStyle = 'red';
        gameCtx.fillRect(food.x, food.y, 10, 10);
    }
    
    function gameOver() {
        clearInterval(gameLoop);
        alert(`Game Over! Your score: ${score}`);
    }
    
    // Keyboard controls for snake game
    document.addEventListener('keydown', function(e) {
        if (!document.getElementById('game-window').classList.contains('active')) {
            // Easter egg: Ctrl+Alt+S to open game
            if (e.ctrlKey && e.altKey && e.key === 's') {
                openApp('game');
                initGame();
            }
            return;
        }
        
        // Prevent arrow keys from scrolling page
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
            e.preventDefault();
        }
        
        // Change direction (but not 180 degrees)
        switch (e.key) {
            case 'ArrowUp':
                if (direction !== 'down') direction = 'up';
                break;
            case 'ArrowDown':
                if (direction !== 'up') direction = 'down';
                break;
            case 'ArrowLeft':
                if (direction !== 'right') direction = 'left';
                break;
            case 'ArrowRight':
                if (direction !== 'left') direction = 'right';
                break;
        }
    });
    
    // Initialize game when window opens
    document.getElementById('game-window').addEventListener('click', function() {
        if (!this.classList.contains('active')) return;
        initGame();
    });
});