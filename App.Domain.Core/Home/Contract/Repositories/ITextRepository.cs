using App.Domain.Core.Home.DTO;
using App.Domain.Core.Home.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.Core.Home.Contract.Repositories
{
    public interface ITextRepository : IRepository<UserTextDTO>
    {
        Task<UserTextDTO> AddAsync(UserTextDTO entity);
        Task<IEnumerable<UserTextDTO>> GetAllAsync();
        Task<IEnumerable<UserTextDTO>> GetByUserIdAsync(int userId);
    }
}
