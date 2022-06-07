import { Link as DomLink, LinkProps } from 'react-router-dom';
import styles from './index.module.scss';

type props = LinkProps;

const Link = (props: props) => {
    return <DomLink className={styles.link} {...props} />;
};

export default Link;
