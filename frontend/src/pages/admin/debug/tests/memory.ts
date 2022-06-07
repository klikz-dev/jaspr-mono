import GenericTest from './generic';

class MemoryTest extends GenericTest {
    async run() {
        super.run();
        // @ts-ignore
        if (performance?.memory) {
            // @ts-ignore
            this.rate = performance?.memory?.jsHeapSizeLimit;
            if (this.rate > 2147352576) {
                this.setStatusLevel('SUCCESS');
                this.resolve(true);
            } else {
                this.setStatusLevel('ERROR');
                this.reject(false);
            }
        } else {
            this.setStatusLevel('WARNING');
            this.details = 'N/A';
        }
        this.progress = 100;
        this.setState(this.getResults());

        return this.promise;
    }
}

export default MemoryTest;
