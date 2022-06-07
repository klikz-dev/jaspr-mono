import logo from 'assets/logo.png';
import styles from './index.module.scss';

interface BannerProps {
    openAccountSetup: () => void;
}

const Banner = ({ openAccountSetup }: BannerProps) => {
    return (
        <div className={styles.banner}>
            <div>
                <img src={logo} alt="Jaspr at Home" />
                <span>Jaspr at Home</span>
            </div>
            <div>
                <p>
                    Access your Stability Plan, Shared Stories, and Comfort &amp; Skills online
                    anytime
                </p>
            </div>
            <div>
                <div className={styles.button} onClick={openAccountSetup}>
                    Setup Account
                </div>
            </div>
        </div>
    );
};

export default Banner;
