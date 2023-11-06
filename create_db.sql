SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `vs5_1`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tbl_progress`
--

CREATE TABLE `tbl_progress` (
  `progress_id` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `answers_total` int(11) NOT NULL,
  `answers_right` int(11) NOT NULL,
  `solved_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `tbl_progress`
--

INSERT INTO `tbl_progress` (`progress_id`, `username`, `answers_total`, `answers_right`, `solved_at`) VALUES
(1, 'Benjamin', 3, 3, '2023-10-28 16:19:41'),
(2, 'Henry', 3, 2, '2023-10-28 16:20:34'),
(3, 'Henry', 3, 2, '2023-10-28 16:21:22'),
(4, 'Henry', 3, 3, '2023-10-29 17:26:31'),
(5, 'Benjamin', 3, 1, '2023-10-30 08:00:21'),
(6, 'Benjamin', 7, 6, '2023-10-30 15:51:13'),
(7, 'Benjamin', 7, 6, '2023-10-31 09:42:38'),
(8, 'Benjamin', 7, 0, '2023-10-31 13:04:00'),
(9, 'Benjamin', 7, 2, '2023-11-02 11:17:53'),
(10, 'Benjamin', 7, 2, '2023-11-02 12:53:56');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tbl_users`
--

CREATE TABLE `tbl_users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `email` varchar(260) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `tbl_users`
--

INSERT INTO `tbl_users` (`user_id`, `username`, `password_hash`, `email`) VALUES
(1, 'Benjamin', '$2b$12$kKpzX.MLyJ/GPRXqgM1kU.epNk2WI2Db9JM.laDrxyGbHzMSjPSdG', 'beni.r04@gmail.com'),
(2, 'Henry', '$2b$12$FoSg2yR9sULMBkSr7Pacn.djlbA0QufZlZCEbgNkVed2QyI.vA.ai', 'henry@yahoo.com'),
(3, 'mathilde', '$2b$12$pU9pVxs8lHRyiP11yoBv/.G1mlux2GfOz29OhxejYTxOPYdS5Hk0C', 'mite@solnet.ch'),
(4, '<b>Hello!</b>', '$2b$12$ISVqx89vXwSH.9rObKO5Kej928RJi0D3HaNo0LhSBZB8pLobect4.', 'aaa@aaa.aaa');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `tbl_progress`
--
ALTER TABLE `tbl_progress`
  ADD PRIMARY KEY (`progress_id`);

--
-- Indizes für die Tabelle `tbl_users`
--
ALTER TABLE `tbl_users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `tbl_progress`
--
ALTER TABLE `tbl_progress`
  MODIFY `progress_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT für Tabelle `tbl_users`
--
ALTER TABLE `tbl_users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
