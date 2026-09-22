class PlaybackState {
    play(manager) {}
    pause(manager) {}
    step(manager) {}
    reset(manager) {}
}

class IdleState extends PlaybackState {
    play(manager) {
        manager.setState(new PlayingState());
        manager.startLoop();
    }
    step(manager) {
        manager.setState(new PausedState());
        manager.advanceOneDay();
    }
}

class PlayingState extends PlaybackState {
    pause(manager) {
        manager.stopLoop();
        manager.setState(new PausedState());
    }
    reset(manager) {
        manager.stopLoop();
        manager.performReset();
        manager.setState(new IdleState());
    }
}

class PausedState extends PlaybackState {
    play(manager) {
        manager.setState(new PlayingState());
        manager.startLoop();
    }
    step(manager) {
        manager.advanceOneDay();
    }
    reset(manager) {
        manager.performReset();
        manager.setState(new IdleState());
    }
}

class CompletedState extends PlaybackState {
    reset(manager) {
        manager.performReset();
        manager.setState(new IdleState());
    }
}

class PlaybackManager {
    constructor(onTickCallback, onCompleteCallback, onResetCallback) {
        this.state = new IdleState();
        this.dailyFrames = [];
        this.currentIndex = 0;
        this.timer = null;
        this.speedMs = 900;
        this.onTick = onTickCallback;
        this.onComplete = onCompleteCallback;
        this.onReset = onResetCallback;
    }

    setState(newState) {
        this.state = newState;
    }

    loadFrames(frames) {
        this.dailyFrames = frames || [];
        this.currentIndex = 0;
        this.setState(new IdleState());
    }

    setSpeed(ms) {
        this.speedMs = ms;
        if (this.state instanceof PlayingState) {
            this.stopLoop();
            this.startLoop();
        }
    }

    play() {
        this.state.play(this);
    }

    pause() {
        this.state.pause(this);
    }

    step() {
        this.state.step(this);
    }

    reset() {
        this.state.reset(this);
    }

    startLoop() {
        if (this.speedMs === 0) {
            while (this.currentIndex < this.dailyFrames.length) {
                this.advanceOneDay();
            }
            return;
        }

        this.timer = setTimeout(() => {
            if (this.currentIndex < this.dailyFrames.length) {
                this.advanceOneDay();
                if (this.currentIndex < this.dailyFrames.length && this.state instanceof PlayingState) {
                    this.startLoop();
                }
            }
        }, this.speedMs);
    }

    stopLoop() {
        if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
        }
    }

    advanceOneDay() {
        if (this.currentIndex >= this.dailyFrames.length) {
            this.setState(new CompletedState());
            if (this.onComplete) this.onComplete();
            return;
        }

        const currentFrame = this.dailyFrames[this.currentIndex];
        this.currentIndex += 1;
        const isFinished = this.currentIndex >= this.dailyFrames.length;

        if (this.onTick) {
            this.onTick(currentFrame, this.currentIndex, this.dailyFrames.length, isFinished);
        }

        if (isFinished) {
            this.stopLoop();
            this.setState(new CompletedState());
            if (this.onComplete) this.onComplete();
        }
    }

    performReset() {
        this.stopLoop();
        this.currentIndex = 0;
        if (this.onReset) this.onReset();
    }
}
