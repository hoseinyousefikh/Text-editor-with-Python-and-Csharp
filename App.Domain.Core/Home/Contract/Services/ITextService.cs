using App.Domain.Core.Home.DTO;
using App.Domain.Core.Home.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.Core.Home.Contract.Services
{
    public interface ITextService
    {
        Task<UserTextDTO> CreateTextAsync(int userId, string content);
        Task<IEnumerable<UserTextDTO>> GetUserTextsAsync(int userId);
    }
}
