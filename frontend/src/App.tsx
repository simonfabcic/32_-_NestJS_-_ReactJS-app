import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from './pages/HomePage'
import Header from './components/Header'

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path='/'  element={<HomePage />}></Route>
      </Routes>
    </BrowserRouter>
    // <BrowserRouter>
    //   <Header />
    //   <Routes>
    //     <Route path='/' element={<HomePage />} exact />
    //     <Route path='about' element={<About />} />
    //     <Route path='posts' element={<Posts />} >
    //       <Route path='new' element={<> <PostsHeader /> <NewPost /> </PostsHeader>} /> {/* A nested route! */}
    //       <Route path=':postId' element={<> <PostsHeader /> <Post /> </PostsHeader>} /> {/* A nested route! */}
    //     </Route>
    //     <Route path="*" element={<h1>Page not fund</h1>}/>
    //   </Routes>
    // </BrowserRouter>
  )
}


// function App() {

//   return (
//     <>
//       <h1 className="text-3xl font-bold underline">
//       Hello world!
//     </h1>
//     </>
//   )
// }

// export default App
