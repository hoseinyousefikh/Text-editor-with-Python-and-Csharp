using App.Domain.Core.Home.Contract.Repositories;
using App.Domain.Core.Home.Contract.Services;
using App.Domain.Core.Home.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.Services.Home.Services
{
    public class TextService : ITextService
    {
        private readonly ITextRepository _textRepository;

        public TextService(ITextRepository textRepository)
        {
            _textRepository = textRepository;
        }

        public async Task<UserTextDTO> CreateTextAsync(int userId, string content)
        {
            var newText = new UserTextDTO
            {
                Content = content,
                UserId = userId,
                CreatedAt = DateTime.UtcNow
            };

            return await _textRepository.AddAsync(newText);
        }

        public async Task<IEnumerable<UserTextDTO>> GetUserTextsAsync(int userId)
        {
            return await _textRepository.GetByUserIdAsync(userId);
        }
    }
}
