using App.Domain.Core.Home.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.Core.Home.Contract.AppServices
{
    public interface ITextAppService
    {
        Task<TextResponseDto> SaveTextAsync(SaveTextRequestDto request, int userId);
        Task<IEnumerable<TextResponseDto>> GetUserTextsAsync(int userId);
    }
}
