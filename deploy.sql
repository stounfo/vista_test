CREATE TABLE `wishlist` (
  `note_id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` char(255) NOT NULL,
  `cost` int unsigned NOT NULL,
  `url` char(255) NOT NULL,
  `description` longtext NULL,
  `tms_create` datetime NOT NULL,
  `tms_update` datetime NOT NULL,
  `status` ENUM('Deleted', 'Done', 'Active') NOT NULL
) AUTO_INCREMENT=1;
