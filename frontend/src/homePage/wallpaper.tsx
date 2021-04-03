import * as React from 'react';

import logo from '../assets/logo.png';
import styles from './styles/wallpaper.module.scss';

const Wallpaper: React.FC = () => {
  return (
    <div className={styles.container}>
      <img className={styles.logo} src={logo} />
    </div>
  );
};

export default Wallpaper;
