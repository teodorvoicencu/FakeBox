import * as React from 'react';

import styles from './styles/gameCard.module.scss';

type Props = {
  title: string;
};

const GameCard: React.FC<Props> = ({ title = 'Joc' }: Props) => {
  return (
    <div className={styles.container}>
      <h2>{title}</h2>
    </div>
  );
};

export default GameCard;
