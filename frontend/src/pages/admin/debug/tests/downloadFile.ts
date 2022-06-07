import axios from 'axios';
import GenericTest from './generic';

class DownloadFileTest extends GenericTest {
    constructor(route: string) {
        super();
        this._route = route;
    }

    async run() {
        super.run();
        axios({
            url: `${this._route}?cache-buster=${Math.floor(Math.random() * 10000000)}`,
            method: 'GET',
            responseType: 'blob',
            onDownloadProgress: function (this: DownloadFileTest, evt: ProgressEvent) {
                this.endTime();
                this.loaded = evt.loaded;
                this.progress = (evt.loaded / evt.total) * 100;
            }.bind(this),
        })
            .then((result) => {
                if (result.status === 200) {
                    this.progress = 100;
                    this.setStatusLevel('SUCCESS');
                }
                this.resolve(true);
            })
            .catch((err) => {
                this.setStatusLevel('ERROR');

                this.details = err.response?.statusText || err.response?.status;
                this.reject(err);
            })
            .finally(() => {
                this.endTime();
                this.finish();
            });

        return this.promise;
    }
}

export default DownloadFileTest;
