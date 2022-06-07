import GenericTest from './generic';

class PerformanceTest extends GenericTest {
    async computePrimeTest() {
        let sieve = [],
            i,
            j,
            primes = [];
        this.rate = 0;
        for (i = 2; i <= 100_000; i += 1) {
            if (!sieve[i]) {
                // i is prime
                primes.push(i);
                const timeTaken = (performance.now() - this._startTime) / 1000;
                this.rate = primes.length;
                if (timeTaken > 5) {
                    return primes.length;
                } else {
                    this.progress = (timeTaken / 5) * 100;
                }
                this.setState(this.getResults());
                for (j = i << 1; j < 100_000; j += i) {
                    sieve[j] = true;
                }
            }
        }
        return primes.length;
    }

    async run() {
        this._startTime = performance.now();
        this.setState(this.getResults());

        this.computePrimeTest().then((numPrimes) => {
            if (numPrimes > 1000) {
                this.progress = 100;
                this.setStatusLevel('SUCCESS');
                this.resolve(true);
            } else if (numPrimes > 500) {
                this.setStatusLevel('WARNING');
                this.reject(false);
            } else {
                this.setStatusLevel('ERROR');
                this.reject(false);
            }
            this._endTime = performance.now();
            this.timing = (this._endTime - this._startTime) / 1000;

            this.finish();
        });

        return this.promise;
    }

    endTime() {
        this._endTime = new Date().getTime();
        this.timing = (this._endTime - this._startTime) / 1000;
        this.setState(this.getResults());
        return this;
    }

    finish() {
        this.complete = true;
        this.setState(this.getResults());
        return this.promise;
    }
}

export default PerformanceTest;
