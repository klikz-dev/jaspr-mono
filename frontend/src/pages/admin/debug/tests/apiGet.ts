import axios from 'axios';
import GenericTest from './generic';

class APIGetTest extends GenericTest {
    warningTime: number;
    constructor(route: string) {
        super();
        this._route = route;
        this.warningTime = 1000;
    }

    async run() {
        super.run();
        axios
            .get(this._route, {
                onDownloadProgress: function (this: APIGetTest, evt: any) {
                    this.endTime();
                    this.progress = (evt.loaded / evt.total) * 100;
                    if (this.timing > this.warningTime) {
                        this.setStatusLevel('WARNING');
                    }
                }.bind(this),
            })
            .then((result) => {
                if (result.status === 200) {
                    this.setStatusLevel('SUCCESS');
                    this.progress = 100;
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

export default APIGetTest;
