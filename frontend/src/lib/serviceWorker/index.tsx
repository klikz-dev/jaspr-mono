import { useContext } from 'react';
import zIndexHelper from 'lib/zIndexHelper';
import StoreContext from 'state/context/store';
import Button from 'components/Button';
import useServiceWorker from './useServiceWorker';
import styles from './index.module.scss';
import useManifest from 'lib/useManifest';

const ServiceWorker = () => {
    const [store] = useContext(StoreContext);
    const { device, user } = store;
    const { userType } = user;
    const { updateAvailable, code, codeType } = device;

    const shouldShowUpdate = userType !== 'patient' && updateAvailable;

    useServiceWorker();

    const update = () => window.location.reload();

    useManifest(code, codeType);

    if (!shouldShowUpdate) {
        return null;
    }

    return (
        <div
            className={styles.container}
            style={{ zIndex: zIndexHelper('technician.update-app-banner') }}
        >
            A new version of Jaspr Health is available
            <Button variant="tertiary" onClick={update}>
                Update
            </Button>
        </div>
    );
};

export default ServiceWorker;
