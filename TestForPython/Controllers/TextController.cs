using App.Domain.Core.Home.Contract.AppServices;
using App.Domain.Core.Home.DTO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace TestForPython.Controllers
{
    [ApiController]
    [Route("api/texts")]
    public class TextController : ControllerBase
    {
        private readonly ITextAppService _textAppService;
        private readonly IConfiguration _configuration;

        public TextController(ITextAppService textAppService, IConfiguration configuration)
        {
            _textAppService = textAppService;
            _configuration = configuration;
        }

        [HttpPost]
        [Authorize]
        public async Task<IActionResult> SaveText([FromBody] SaveTextRequestDto request)
        {
            var userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier).Value);
            var response = await _textAppService.SaveTextAsync(request, userId);
            return Ok(response);
        }

        [HttpGet]
        [Authorize]
        public async Task<IActionResult> GetUserTexts()
        {
            var userId = int.Parse(User.FindFirst(ClaimTypes.NameIdentifier).Value);
            var texts = await _textAppService.GetUserTextsAsync(userId);
            return Ok(texts);
        }
    }
}
