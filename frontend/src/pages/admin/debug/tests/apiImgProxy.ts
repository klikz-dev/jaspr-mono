import GenericTest from './generic';

class ImgProxyTest extends GenericTest {
    constructor(route: string) {
        super();
        this._route = route;
    }

    async run() {
        super.run();
        this.startTime();
        const img = new Image();
        img.onload = (e) => {
            this.setStatusLevel('SUCCESS');
            this.progress = 100;
            this.endTime();
            this.resolve(true);
        };
        img.onerror = (e) => {
            this.setStatusLevel('ERROR');
            this.endTime();
            this.reject(false);
        };
        img.onabort = (e) => {
            this.setStatusLevel('ERROR');
            this.endTime();
            this.reject(false);
        };
        img.src = `${this._route}?cache-buster=${Math.floor(Math.random() * 10000000)}`;

        return this.promise;
    }
}

export default ImgProxyTest;
