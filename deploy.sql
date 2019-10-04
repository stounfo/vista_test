CREATE TABLE `wishlist` (
  `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` char(255) NOT NULL,
  `cost` int unsigned NOT NULL,
  `url` char(255) NOT NULL,
  `note` longtext NULL,
  `status` ENUM('Deleted', 'Done', 'Active')
) AUTO_INCREMENT=1;
