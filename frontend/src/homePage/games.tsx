import * as React from 'react';

import GameCard from './gameCard';
import styles from './styles/games.module.scss';

const Games: React.FC = () => {
  return (
    <div className={styles.container}>
      <GameCard title={'Nenea Nae'} />
      <GameCard title={'Nenea Nae'} />
      <GameCard title={'Nenea Nae'} />
      <GameCard title={'Nenea Nae'} />
    </div>
  );
};

export default Games;
