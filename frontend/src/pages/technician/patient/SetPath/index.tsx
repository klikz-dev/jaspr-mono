import Modal, { Styles } from 'react-modal';
import { useHistory, useRouteMatch } from 'lib/router';

import zIndexHelper from 'lib/zIndexHelper';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { Activity } from 'state/types';
import AddActivities from '../AddActivities';

const modalStyle: Styles = {
    overlay: {
        marginTop: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0,0,0,0.4)',
        zIndex: zIndexHelper('technician.set-path'),
    },
    content: {
        position: 'relative',
        display: 'flex',
        justifyContent: 'space-around',
        flexDirection: 'column',
        border: 'none',
        backgroundColor: '#ffffff',
        padding: 35,
        maxWidth: '800px',
        width: '95%',
        boxShadow: '0px 1px 4px rgba(0, 0, 0, 0.25)',
        overflow: 'hidden',
        inset: 'inherit',
        borderRadius: 3,
    },
};

const fullModalStyle: Styles = {
    overlay: {
        display: 'flex',
        backgroundColor: 'rgba(255,255,255,1)',
        marginTop: 97,
    },
    content: {
        position: 'relative',
        display: 'flex',
        border: 'none',
        backgroundColor: '#ffffff',
        padding: 35,
        inset: 'inherit',
    },
};

interface SetPathProps {
    patient: PatientGetResponse;
    activities: Activity[];
    setActivities: (activities: Activity[]) => void;
    getPatientData: () => void;
    stabilityPlanLabel: string;
}

const SetPath = ({
    patient,
    activities = [],
    setActivities,
    getPatientData = () => {},
    stabilityPlanLabel = 'Stability Plan',
}: SetPathProps) => {
    const initial = activities.length === 0;
    const history = useHistory();
    const match = useRouteMatch();

    const close = () => history.replace(match.url.split('/').slice(0, -1).join('/'));

    return (
        <Modal isOpen style={initial ? fullModalStyle : modalStyle}>
            <AddActivities
                patient={patient}
                activities={activities}
                setActivities={setActivities}
                getPatientData={getPatientData}
                close={close}
                stabilityPlanLabel={stabilityPlanLabel}
            />
        </Modal>
    );
};

export default SetPath;
