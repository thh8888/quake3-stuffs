CREATE TABLE IF NOT EXISTS players (
    playername VARCHAR(64),
    kills INT NOT NULL,
    deaths INT NOT NULL,
    suicides INT NOT NULL,
    hand INT NOT NULL,
    machinegun INT NOT NULL,
    shotgun INT NOT NULL,
    grenade INT NOT NULL,
    rocket INT NOT NULL,
    railgun INT NOT NULL,
    lightning INT NOT NULL,
    plasma INT NOT NULL,
    bfg INT NOT NULL,
    matches INT NOT NULL,
    UNIQUE KEY (playername)
);
