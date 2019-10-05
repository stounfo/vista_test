CREATE TABLE `wishlist` (
  `note_id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` char(255) NOT NULL,
  `cost` int unsigned NOT NULL,
  `url` char(255) NOT NULL,
  `description` longtext NOT NULL,
  `tms_create` datetime NOT NULL,
  `tms_update` datetime NOT NULL,
  `status` ENUM('Deleted', 'Done', 'Active') NOT NULL
) AUTO_INCREMENT=1;

INSERT INTO `wishlist` (`name`, `cost`, `url`, `description`, `tms_create`, `tms_update`, `status`)
VALUES ('My GitHub', '0', 'https://github.com/stounfo', 'This is my GitHub link.', '2019-10-04 20:30:00', '2019-10-04 20:30:00', 3);