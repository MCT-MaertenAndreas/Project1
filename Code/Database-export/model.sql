-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema water_dispenser
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema water_dispenser
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `water_dispenser` ;
USE `water_dispenser` ;

-- -----------------------------------------------------
-- Table `water_dispenser`.`core_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_users` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `password` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `water_dispenser`.`core_token_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_token_types` (
  `token_type_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `short` VARCHAR(8) NULL,
  `long` VARCHAR(45) NULL,
  PRIMARY KEY (`token_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `water_dispenser`.`core_tokens`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_tokens` (
  `token_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `token` VARCHAR(128) NOT NULL,
  `token_type` INT UNSIGNED NOT NULL,
  `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`token_id`),
  UNIQUE INDEX `token_UNIQUE` (`token` ASC) ,
  INDEX `fk_core_tokens_core_token_types_idx` (`token_type` ASC) ,
  CONSTRAINT `fk_core_tokens_core_token_types`
    FOREIGN KEY (`token_type`)
    REFERENCES `water_dispenser`.`core_token_types` (`token_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `water_dispenser`.`core_users_sessions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_users_sessions` (
  `user_id` INT UNSIGNED NOT NULL,
  `token_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`user_id`, `token_id`),
  INDEX `fk_core_users_has_core_tokens_core_users1_idx` (`user_id` ASC) ,
  INDEX `fk_core_users_sessions_core_tokens1_idx` (`token_id` ASC) ,
  CONSTRAINT `fk_core_users_has_core_tokens_core_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `water_dispenser`.`core_users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_core_users_sessions_core_tokens1`
    FOREIGN KEY (`token_id`)
    REFERENCES `water_dispenser`.`core_tokens` (`token_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `water_dispenser`.`core_sensor_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_sensor_type` (
  `sensor_type_id` INT UNSIGNED NOT NULL,
  `code_name` VARCHAR(64) NULL,
  `name` VARCHAR(45) NULL,
  `description` VARCHAR(256) NULL,
  PRIMARY KEY (`sensor_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `water_dispenser`.`core_sensors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_sensors` (
  `sensor_id` INT UNSIGNED NOT NULL,
  `hint_name` VARCHAR(45) NULL,
  `sensor_type` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`sensor_id`),
  INDEX `fk_core_sensors_core_sensor_type1_idx` (`sensor_type` ASC) ,
  CONSTRAINT `fk_core_sensors_core_sensor_type1`
    FOREIGN KEY (`sensor_type`)
    REFERENCES `water_dispenser`.`core_sensor_type` (`sensor_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `water_dispenser`.`core_measurement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `water_dispenser`.`core_measurement` (
  `measurement_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `value` VARCHAR(256) NULL,
  `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `sensor_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`measurement_id`, `sensor_id`),
  INDEX `fk_core_measurement_core_sensors1_idx` (`sensor_id` ASC) ,
  CONSTRAINT `fk_core_measurement_core_sensors1`
    FOREIGN KEY (`sensor_id`)
    REFERENCES `water_dispenser`.`core_sensors` (`sensor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
