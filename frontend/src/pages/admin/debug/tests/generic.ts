class Test {
    _route: string;
    statusText: string;
    status: -1 | 0 | 1 | 2;
    progress: number;
    complete: boolean;
    timing: number;
    details: string;
    loaded: number;
    promise: Promise<any>;
    resolve!: (value: any) => void;
    reject!: (reason?: any) => void;
    state: {};
    setState!: (state: any) => void;
    _startTime: number;
    _endTime: number;
    rate: number;
    time: number;

    constructor() {
        this._route = '';
        this._startTime = 0;
        this._endTime = 0;
        this.time = 0;
        this.state = {};
        this.statusText = '';
        this.status = -1;
        this.progress = 0;
        this.complete = false;
        this.timing = 0;
        this.details = '';
        this.loaded = 0;
        this.rate = 0;
        this.promise = new Promise((resolve, reject) => {
            this.resolve = resolve;
            this.reject = reject;
        });
    }

    static get _LEVELS(): {
        SUCCESS: 0;
        WARNING: 1;
        ERROR: 2;
    } {
        return {
            SUCCESS: 0,
            WARNING: 1,
            ERROR: 2,
        };
    }

    setter(setState: any) {
        this.setState = setState;
        return this;
    }

    run() {
        this.startTime();
        return this.promise;
    }

    startTime() {
        this._startTime = new Date().getTime();
        return this;
    }

    endTime(): Test {
        this._endTime = new Date().getTime();
        this.timing = (this._endTime - this._startTime) / 1000;
        this.rate = this.loaded / 1024.0 / 1024.0 / this.timing / 0.125; // MB/s
        this.setState(this.getResults());
        return this;
    }
    // @ts-ignore
    setStatusLevel(status: keyof _LEVELS) {
        // @ts-ignore
        const level = Test._LEVELS[status];
        // @ts-ignore
        this.status = Math.max(level, this.status);
        if (this.status === level) {
            // @ts-ignore
            this.statusText = status;
        }
        this.setState(this.getResults());
        return this;
    }

    getResults() {
        return {
            // @ts-ignore
            status: Test._LEVELS[this.status],
            statusText: this.statusText,
            progress: this.progress,
            complete: this.complete,
            details: this.details,
            timing: this.timing,
            rate: this.rate,
        };
    }

    finish() {
        this.complete = true;
        this.setState(this.getResults());
        if (this.time > 1 && this.rate < 3) {
            this.setStatusLevel('WARNING');
        }
        return this.promise;
    }
}

export default Test;
