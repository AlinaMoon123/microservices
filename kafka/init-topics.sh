#!/bin/bash
set -e

echo "Waiting for Kafka..."
cub kafka-ready -b kafka:9092 1 30

echo "Creating topics..."

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic order.events \
  --partitions 8 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic inventory.commands \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic payment.commands \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic payment.retry.1 \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic payment.retry.2 \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic payment.dlq \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic inventory.retry.1 \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic inventory.retry.2 \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic inventory.dlq \
  --partitions 4 \
  --replication-factor 1

kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --topic notification.command \
  --partitions 4 \
  --replication-factor 1

echo "Topics created"
