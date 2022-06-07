import Button from 'components/Button';
import { toast as hotToast, DefaultToastOptions, resolveValue } from 'react-hot-toast';
import styles from './index.module.scss';

type Opts =
    | (DefaultToastOptions & {
          title?: string;
          actionLabel?: string;
          action?: () => void;
          dark?: boolean;
      })
    | undefined;

const Msg = (props: any) => {
    const { title, message, actionLabel = 'Okay', action, dark = false, msg, ...t } = props;
    return (
        <div className={`${styles.toast} ${dark ? styles.dark : ''} `}>
            <div className={`${styles.content} typography--body2`}>
                {title && <span className="typography--body1">{title}</span>}
                {resolveValue(msg, t)}
            </div>
            <Button
                variant="tertiary"
                onClick={() => (action ? action() : hotToast.dismiss(t.id))}
                dark={dark}
            >
                {actionLabel}
            </Button>
        </div>
    );
};

const customToast = {
    success: (msg: string, opts?: Opts) =>
        hotToast.custom((t) => <Msg {...t} {...opts} msg={msg} />),
    error: (msg: string, opts?: Opts) => hotToast.custom((t) => <Msg {...t} {...opts} msg={msg} />),
};

export default customToast;
