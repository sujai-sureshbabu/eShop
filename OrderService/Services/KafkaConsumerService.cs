using Confluent.Kafka;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;

namespace OrderService.Services;

public class KafkaConsumerService : BackgroundService
{
    private readonly KafkaSettings _settings;
    private readonly ILogger<KafkaConsumerService> _logger;
    private IConsumer<Null, string> _consumer;

    public KafkaConsumerService(IOptions<KafkaSettings> options, ILogger<KafkaConsumerService> logger)
    {
        _settings = options.Value;
        _logger = logger;

        var config = new ConsumerConfig
        {
            BootstrapServers = _settings.BootstrapServers,
            GroupId = _settings.GroupId,
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoCommit = true
        };

        _consumer = new ConsumerBuilder<Null, string>(config).Build();
        _consumer.Subscribe(_settings.Topic);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            _logger.LogInformation("[OrderService] Waiting for messages...");
            // Consume messages from Kafka
            try
            {
                var message = _consumer.Consume(stoppingToken);
                _logger.LogInformation($"[OrderService] Received message: {message.Message.Value}");
            }
            catch (OperationCanceledException) { break; }
            catch (ConsumeException ex)
            {
                _logger.LogError($"Consume error: {ex.Message}");
            }
        }
    }

    public override void Dispose()
    {
        _consumer?.Close();
        _consumer?.Dispose();
        base.Dispose();
    }
}
