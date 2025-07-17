using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Confluent.Kafka;
using ProductService;
using Microsoft.Extensions.Options;

namespace ProductService.Controllers;
[ApiController]
[Route("api/[controller]")]
public class ProductController : ControllerBase
{
    private readonly ILogger<ProductController> _logger;
    private readonly KafkaSettings _kafkaSettings;
    private readonly IProducer<Null, string> _producer;
    public ProductController(IOptions<KafkaSettings> kafkaSettings, ILogger<ProductController> logger)
    {
        _kafkaSettings = kafkaSettings.Value;
        _logger = logger;

        var config = new ProducerConfig { BootstrapServers = _kafkaSettings.BootstrapServers };
        _producer = new ProducerBuilder<Null, string>(config).Build();
    }

    [HttpGet]
    public IActionResult GetProducts()
    {
        _logger.LogInformation("Fetching products");
        // Simulate fetching products
        return Ok(new { Products = new[] { "Product1", "Product2" } });
    }
    [HttpPost("publish")]
    public async Task<IActionResult> PublishProductEvent([FromBody] string message)
    {
        if (string.IsNullOrEmpty(message))
            return BadRequest("Message cannot be empty.");

        _logger.LogInformation($"Publishing message: {message}");
        var result = await _producer.ProduceAsync(_kafkaSettings.Topic, new Message<Null, string> { Value = message });

        return Ok(result.TopicPartitionOffset.ToString());
    }



}