import Modal, { Styles } from 'react-modal';
import { Link } from 'lib/router';
import printerIcon from 'assets/printer.svg';
import styles from './index.module.scss';
import { formatDate } from 'lib/helpers';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import Segment, { AnalyticNames } from 'lib/segment';

const modalStyle: Styles = {
    content: {
        position: 'relative',
        display: 'flex',
        flex: 1,
        border: 'none',
        backgroundColor: '#ffffff',
        padding: 35,
        inset: 'inherit',
    },
};

interface ReportProps {
    patient: PatientGetResponse;
    report: {
        noteType: 'stability_plan' | 'narrative_note';
        created: string;
        note: string;
    };
}

const Report = ({ patient, report }: ReportProps) => {
    const print = () => {
        Segment.track(AnalyticNames.TECHNICIAN_PRINTED_REPORT, { type: report?.noteType });
        window.print();
    };

    return (
        <Modal isOpen style={modalStyle} overlayClassName={styles.modalContainer}>
            <div className={styles.container}>
                <header>
                    {report?.noteType === 'stability_plan' && <span>Stability Plan</span>}
                    {report?.noteType === 'narrative_note' && <span>Narrative Note</span>}
                    <img src={printerIcon} alt="Print Note" onClick={print} />
                    <Link className={styles.close} to={`/technician/patients/${patient.id}/`}>
                        Close
                    </Link>
                </header>
                <div className={styles.date}>{formatDate(report.created)}</div>
                <div className={styles.note}>{report.note}</div>
            </div>
        </Modal>
    );
};

export default Report;
