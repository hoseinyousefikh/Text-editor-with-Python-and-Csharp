using App.Domain.Core.Home.Contract.AppServices;
using App.Domain.Core.Home.Contract.Services;
using App.Domain.Core.Home.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.AppServices.Home.AppServices
{
    public class TextAppService : ITextAppService
    {
        private readonly ITextService _textService;

        public TextAppService(ITextService textService)
        {
            _textService = textService;
        }

        public async Task<TextResponseDto> SaveTextAsync(SaveTextRequestDto request, int userId)
        {
            var text = await _textService.CreateTextAsync(userId, request.Content);

            return new TextResponseDto
            {
                TextId = text.TextId,
                Content = text.Content,
                CreatedAt = text.CreatedAt,
                UpdatedAt = text.UpdatedAt
            };
        }

        public async Task<IEnumerable<TextResponseDto>> GetUserTextsAsync(int userId)
        {
            var texts = await _textService.GetUserTextsAsync(userId);

            return texts.Select(t => new TextResponseDto
            {
                TextId = t.TextId,
                Content = t.Content,
                CreatedAt = t.CreatedAt,
                UpdatedAt = t.UpdatedAt
            });
        }
    }
}
