import axios from 'axios';
import GenericTest from './generic';

class APIHeadTest extends GenericTest {
    constructor(route: string) {
        super();
        this._route = route;
    }

    async run() {
        super.run();
        axios
            .head(this._route)
            .then((result) => {
                if (result.status === 200) {
                    this.progress = 100;
                    this.setStatusLevel('SUCCESS');
                }
                this.resolve(true);
            })
            .catch((err) => {
                this.setStatusLevel('ERROR');
                this.details = err.response?.statusText;
                this.reject(err);
            })
            .finally(() => {
                this.endTime();
                this.finish();
            });

        return this.promise;
    }
}

export default APIHeadTest;
