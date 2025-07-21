import json
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

import time
from kafka.errors import NoBrokersAvailable, KafkaError

def wait_for_kafka(bootstrap_servers, retries=10, delay=3):
    from kafka import KafkaAdminClient
    for i in range(retries):
        try:
            client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            client.close()
            print("Kafka is ready!")
            return True
        except NoBrokersAvailable:
            print(f"Kafka not ready yet, retrying in {delay}s... ({i+1}/{retries})")
            time.sleep(delay)
        except KafkaError as e:
            print(f"Kafka error: {e}")
            time.sleep(delay)
    return False

def create_topics_from_file(config_file, bootstrap_servers):
    with open(config_file) as f:
        topics_config = json.load(f)

    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    new_topics = []
    for t in topics_config:
        configs = t.get("configs", {})
        topic = NewTopic(
            name=t["name"],
            num_partitions=t["partitions"],
            replication_factor=t["replication_factor"],
            topic_configs=configs
        )
        new_topics.append(topic)

    try:
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
        print(f"Created topics: {[t.name for t in new_topics]}")
    except TopicAlreadyExistsError as e:
        print("Some topics already exist. Skipping those.")
    except Exception as e:
        print(f"Error creating topics: {e}")
    finally:
        admin_client.close()

if __name__ == "__main__":
    bootstrap_servers = "kafka:9092"
    if not wait_for_kafka(bootstrap_servers):
        print("Kafka did not become ready, exiting.")
        exit(1)

    create_topics_from_file("topics.json", bootstrap_servers=bootstrap_servers)
